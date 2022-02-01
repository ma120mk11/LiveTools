import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, Observable, tap } from 'rxjs';
import { HandleError, HttpErrorHandler } from 'src/app/services/http-error-handler.service';
import { ISong } from './song';

@Injectable()
export class SongsService {
  songsUrl = "http://localhost:8000/songs"
  private handleError: HandleError;

  constructor(
    private http: HttpClient,
    httpErrorHandler: HttpErrorHandler) {
      this.handleError = httpErrorHandler.createHandleError("SongBookComponent");
    }

  getSongs(): Observable<ISong[]> {
    
    
    console.log("getting songs...")
    return this.http.get<ISong[]>(this.songsUrl)
    .pipe(
      tap(
        data => console.log(data)
      )
    );
  }
  
  }
  // catchError(this.handleError("getSongs", []))