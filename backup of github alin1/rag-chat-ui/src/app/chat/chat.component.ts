import { Component, OnInit, ChangeDetectorRef } from '@angular/core'; // <-- Added ChangeDetectorRef here
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Injectable, NgZone } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { MarkdownModule } from 'ngx-markdown';

export interface StreamResponse {
  type: 'token' | 'sources' | 'error' | 'done';
  value?: any;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
  timestamp: Date;
  thinkTime?: number; // Time until the first word is typed
  totalTime?: number; // Total time from start to finish
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient, private zone: NgZone) {}

  streamChat(message: string, subject: string): Observable<StreamResponse> {
    return new Observable((observer) => {
      const url = `${this.apiUrl}/chat/stream?message=${encodeURIComponent(message)}&subject=${encodeURIComponent(subject)}`;
      const eventSource = new EventSource(url);

      eventSource.onmessage = (event) => {
        this.zone.run(() => {
          const data = JSON.parse(event.data);
          if (data.sources) {
            observer.next({ type: 'sources', value: data.sources });
          } else if (data.token) {
            observer.next({ type: 'token', value: data.token });
          } else if (data.done) {
            observer.next({ type: 'done' });
            observer.complete();
            eventSource.close();
          } else if (data.error) {
            observer.next({ type: 'error', value: data.error });
            observer.complete();
            eventSource.close();
          }
        });
      };

      eventSource.onerror = (error) => {
        this.zone.run(() => {
          observer.next({ type: 'error', value: 'Connection lost or server error.' });
          observer.complete();
          eventSource.close();
        });
      };

      return () => {
        eventSource.close();
      };
    });
  }

  clearMemory(): Observable<any> {
    return this.http.post(`${this.apiUrl}/clear`, {});
  }
}

// ... (keep your imports and interfaces exactly the same) ...

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, MarkdownModule],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.css'
})
export class ChatComponent implements OnInit {
  messages: ChatMessage[] = [];
  userInput: string = '';
  selectedSubject: string = 'rtl';
  isLoading: boolean = false;
  isStreaming: boolean = false;
  subjects: string[] = ['general', 'english', 'maths', 'python', 'rtl'];

  timerInterval: any; // <-- ADD THIS to hold our stopwatch

  constructor(private chatService: ChatService, private cd: ChangeDetectorRef) {}

  ngOnInit(): void {}

  sendMessage() {
    if (!this.userInput.trim() || this.isStreaming) return;

    // 1. Setup the User Message
    const userMsg: ChatMessage = {
      role: 'user',
      content: this.userInput,
      timestamp: new Date()
    };
    this.messages.push(userMsg);
    
    const messageToSend = this.userInput;
    this.userInput = '';
    this.isStreaming = true;

    // 2. Instantly push the Assistant Bubble so it animates in immediately
    const assistantMsg: ChatMessage = {
      role: 'assistant',
      content: '',
      sources: [],
      timestamp: new Date(),
      thinkTime: 0.0,
      totalTime: 0.0
    };
    this.messages.push(assistantMsg);

    // 3. START THE LIVE STOPWATCH
    const startTime = Date.now();
    let hasCalculatedTime = false; 

    this.timerInterval = setInterval(() => {
      const elapsed = (Date.now() - startTime) / 1000;
      assistantMsg.totalTime = elapsed; // Total time always ticks up
      
      if (!hasCalculatedTime) {
        assistantMsg.thinkTime = elapsed; // Think time only ticks up if it hasn't typed yet
      }
      this.cd.detectChanges(); // Tell Angular to update the screen!
    }, 100);

    // 4. Call the Backend
    this.chatService.streamChat(messageToSend, this.selectedSubject).subscribe({
      next: (res: StreamResponse) => {
        
        // LAP 1: The first word arrives! Lock the Think Time.
        if (!hasCalculatedTime && res.type === 'token' && res.value) {
          hasCalculatedTime = true;
        }

        if (res.type === 'sources') {
          assistantMsg.sources = res.value;
        } else if (res.type === 'token') {
          assistantMsg.content += res.value;
        } else if (res.type === 'error') {
          assistantMsg.content = `Error: ${res.value}`;
        }
        this.cd.detectChanges();
      },
      error: (err) => {
        clearInterval(this.timerInterval); // Stop the watch on error
        this.isStreaming = false;
        this.cd.detectChanges();
      },
      complete: () => {
        clearInterval(this.timerInterval); // FINISH LINE: Stop the watch!
        this.isStreaming = false;
        this.cd.detectChanges();
      }
    });
  }

  clearChat(): void {
    this.messages = [];
    this.chatService.clearMemory().subscribe();
  }
}