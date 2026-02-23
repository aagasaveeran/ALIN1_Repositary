import { Component, OnInit } from '@angular/core';
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
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient, private zone: NgZone) {}

  // 1. We added 'subject: string' here so it expects the second argument
  streamChat(message: string, subject: string): Observable<StreamResponse> {
    return new Observable((observer) => {
      
      // 2. We added &subject= to the URL to tell Python which DB to use
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

  constructor(private chatService: ChatService) {}

  ngOnInit(): void {}

  sendMessage(): void {
    if (!this.userInput.trim() || this.isStreaming) {
      return;
    }

    const userMessage: ChatMessage = {
      role: 'user',
      content: this.userInput,
      timestamp: new Date()
    };

    this.messages.push(userMessage);
    const message = this.userInput;
    this.userInput = '';
    this.isStreaming = true;

    const assistantMessage: ChatMessage = {
      role: 'assistant',
      content: '',
      sources: [],
      timestamp: new Date()
    };

    this.messages.push(assistantMessage);

    this.chatService.streamChat(message, this.selectedSubject).subscribe({
      next: (response: StreamResponse) => {
        if (response.type === 'token' && assistantMessage.content !== undefined) {
          assistantMessage.content += response.value;
        } else if (response.type === 'sources') {
          assistantMessage.sources = response.value;
        } else if (response.type === 'done') {
          this.isStreaming = false;
        } else if (response.type === 'error') {
          assistantMessage.content = `Error: ${response.value}`;
          this.isStreaming = false;
        }
      },
      error: () => {
        assistantMessage.content = 'Error: Failed to get response from server.';
        this.isStreaming = false;
      }
    });
  }

  clearChat(): void {
    this.messages = [];
    this.chatService.clearMemory().subscribe();
  }
}