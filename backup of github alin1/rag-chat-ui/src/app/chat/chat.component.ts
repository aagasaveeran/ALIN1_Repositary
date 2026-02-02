import { Component, OnInit, ViewChild, ElementRef, AfterViewChecked, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MarkdownModule } from 'ngx-markdown';
import { ChatService, ChatMessage, StreamResponse } from '../services/chat.service';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, MarkdownModule],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit, AfterViewChecked {
  @ViewChild('scrollContainer') private scrollContainer!: ElementRef;

  messages: ChatMessage[] = [];
  userInput = '';
  isStreaming = false;

  constructor(
    private chatService: ChatService,
    private cd: ChangeDetectorRef
  ) {}

  ngOnInit() {}

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  scrollToBottom(): void {
    try {
      if (this.scrollContainer) {
        this.scrollContainer.nativeElement.scrollTop = this.scrollContainer.nativeElement.scrollHeight;
      }
    } catch (err) {}
  }

  sendMessage() {
    if (!this.userInput.trim() || this.isStreaming) return;

    const userMsg: ChatMessage = {
      role: 'user',
      content: this.userInput,
      timestamp: new Date()
    };

    this.messages.push(userMsg);
    const messageToSend = this.userInput;
    this.userInput = '';
    this.isStreaming = true;

    const assistantMsg: ChatMessage = {
      role: 'assistant',
      content: '',
      sources: [],
      timestamp: new Date()
    };
    this.messages.push(assistantMsg);

    this.chatService.streamChat(messageToSend).subscribe({
      next: (res: StreamResponse) => {
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
        this.isStreaming = false;
        this.cd.detectChanges();
      },
      complete: () => {
        this.isStreaming = false;
        this.cd.detectChanges();
      }
    });
  }

  clearChat() {
    this.chatService.clearMemory().subscribe(() => {
      this.messages = [];
    });
  }
}