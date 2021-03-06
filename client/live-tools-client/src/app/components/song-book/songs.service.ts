import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, Observable, tap, throwError } from 'rxjs';
import { HandleError, HttpErrorHandler } from 'src/app/services/http-error-handler.service';
import { environment } from 'src/environments/environment';
import { ISong } from './song';

@Injectable()
export class SongsService {
  private handleError: HandleError;

  constructor(
    private http: HttpClient,
    httpErrorHandler: HttpErrorHandler) {
      this.handleError = httpErrorHandler.createHandleError("SongBookComponent");
    }

  getSongs(includeHidden: boolean = false): Observable<ISong[]> {
    
    console.log("getting songs...")
    return this.http.get<ISong[]>(`${environment.apiEndpoint}/songs`,{params: {"include_hidden": includeHidden}})
    .pipe(
      tap(
        // data => console.log(data)
        )
      );
    }
  

  updateLyric(songId: number, lyrics: string): Observable<any>{
    console.log("Lyrics...")
    return this.http.put(`${environment.apiEndpoint}/songs/${songId}/lyrics`, lyrics)
    .pipe(
      catchError((error) => {
        console.log("");
        return throwError(() => new Error("Error updating lyrics"));
      })
    )
  }
}
  // catchError(this.handleError("getSongs", []))