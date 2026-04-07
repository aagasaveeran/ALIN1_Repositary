import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  sources?: any[]; // Supports {id, topic} objects
  timestamp: Date;
  thinkTime?: number; 
  totalTime?: number; 
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

  /**
   * Upgraded to use fetch POST for History-Aware Streaming.
   * This ensures we can send the full chat history without URL length limits.
   */
  streamChat(message: string, subject: string, history: ChatMessage[]): Observable<StreamResponse> {
    return new Observable(observer => {
      const url = `${this.apiUrl}/chat/stream?message=${encodeURIComponent(message)}&subject=${encodeURIComponent(subject)}`;
      
      // We clean the history to only send role and content to the backend
      const cleanHistory = history.map(h => ({ role: h.role, content: h.content }));

      const controller = new AbortController();
      
      fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(cleanHistory),
        signal: controller.signal
      }).then(async (response) => {
        if (!response.body) throw new Error('No response body');
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        try {
          while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            
            // SSE chunks usually come as "data: {...}"
            const lines = chunk.split('\n');
            for (const line of lines) {
              if (line.startsWith('data: ')) {
                const jsonStr = line.replace('data: ', '').trim();
                if (!jsonStr) continue;

                const data = JSON.parse(jsonStr);

                if (data.sources) {
                  observer.next({ type: 'sources', value: data.sources });
                } else if (data.token) {
                  observer.next({ type: 'token', value: data.token });
                } else if (data.done) {
                  observer.next({ type: 'done', value: null });
                  observer.complete();
                } else if (data.error) {
                  observer.next({ type: 'error', value: data.error });
                  observer.complete();
                }
              }
            }
          }
        } catch (e) {
          observer.error(e);
        }
      }).catch(err => {
        observer.error('Connection lost or server error');
      });

      return () => controller.abort(); // Cleanup if unsubscribed
    });
  }

  clearMemory() {
    return this.http.post(`${this.apiUrl}/clear`, {});
  }
}