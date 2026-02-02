import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
  timestamp: Date;
}

export interface StreamResponse {
  type: 'sources' | 'token' | 'done' | 'error';
  value: any;
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  getBooks(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/books`);
  }

  streamChat(message: string): Observable<StreamResponse> {
    return new Observable(observer => {
      const url = `${this.apiUrl}/chat/stream?message=${encodeURIComponent(message)}`;
      const eventSource = new EventSource(url);

      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          
          if (data.sources) {
            observer.next({ type: 'sources', value: data.sources });
          } else if (data.token) {
            observer.next({ type: 'token', value: data.token });
          } else if (data.done) {
            observer.next({ type: 'done', value: null });
            eventSource.close();
            observer.complete();
          } else if (data.error) {
            observer.next({ type: 'error', value: data.error });
            eventSource.close();
            observer.complete();
          }
        } catch (e) {
          console.error('Parsing error', e);
        }
      };

      eventSource.onerror = (error) => {
        eventSource.close();
        observer.error('Connection lost');
      };

      return () => eventSource.close();
    });
  }

  clearMemory() {
    return this.http.post(`${this.apiUrl}/clear`, {});
  }
}