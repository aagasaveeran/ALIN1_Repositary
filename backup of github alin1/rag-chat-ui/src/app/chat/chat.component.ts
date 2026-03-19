import { Component, OnInit, ChangeDetectorRef } from '@angular/core'; 
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MarkdownModule } from 'ngx-markdown';
import { ChatService, ChatMessage, StreamResponse } from '../services/chat.service';

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
  
  // Updated to match your backend DB_MAP
  subjects: string[] = ['rtl', 'python', 'maths', 'english'];

  timerInterval: any; 

  constructor(private chatService: ChatService, private cd: ChangeDetectorRef) {}

  ngOnInit(): void {}

  sendMessage() {
    if (!this.userInput.trim() || this.isStreaming) return;

    // 1. Capture user message
    const userMsg: ChatMessage = {
      role: 'user',
      content: this.userInput,
      timestamp: new Date()
    };
    
    // 2. Clone the history BEFORE adding the current message 
    // (The backend usually wants the history leading up to the prompt)
    const historyContext = [...this.messages];

    this.messages.push(userMsg);
    
    const messageToSend = this.userInput;
    this.userInput = '';
    this.isStreaming = true;

    // 3. Prepare placeholder for Assistant
    const assistantMsg: ChatMessage = {
      role: 'assistant',
      content: '',
      sources: [],
      timestamp: new Date(),
      thinkTime: 0.0,
      totalTime: 0.0
    };
    this.messages.push(assistantMsg);

    const startTime = Date.now();
    let hasCalculatedTime = false; 

    // 4. Start Metrics Timer
    this.timerInterval = setInterval(() => {
      const elapsed = (Date.now() - startTime) / 1000;
      assistantMsg.totalTime = elapsed; 
      
      if (!hasCalculatedTime) {
        assistantMsg.thinkTime = elapsed; 
      }
      this.cd.detectChanges(); 
    }, 100);

    // 5. Call Service with the new History Parameter
    this.chatService.streamChat(messageToSend, this.selectedSubject, historyContext).subscribe({
      next: (res: StreamResponse) => {
        // Stop "Thinking" metric when the first real token arrives
        if (!hasCalculatedTime && res.type === 'token' && res.value) {
          hasCalculatedTime = true;
        }

        if (res.type === 'sources') {
          assistantMsg.sources = res.value;
        } else if (res.type === 'token') {
          assistantMsg.content += res.value;
        } else if (res.type === 'error') {
          assistantMsg.content = `⚠️ Connection Error: ${res.value}`;
        }
        this.cd.detectChanges();
      },
      error: (err) => {
        this.stopTimer();
        assistantMsg.content = "❌ The server connection was lost.";
        this.isStreaming = false;
        this.cd.detectChanges();
      },
      complete: () => {
        this.stopTimer();
        this.isStreaming = false;
        this.cd.detectChanges();
      }
    });
  }

  private stopTimer() {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
    }
  }

  clearChat(): void {
    this.messages = [];
    this.chatService.clearMemory().subscribe({
      next: () => console.log("Session reset on backend"),
      error: (err) => console.error("Clear failed", err)
    });
  }
}