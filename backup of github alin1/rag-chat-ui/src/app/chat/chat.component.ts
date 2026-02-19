import { Injectable, NgZone } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

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