import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { EngineComponent } from './components/engine/engine.component';
import { PageNotFoundComponent } from './components/page-not-found/page-not-found.component';
import { NavigationComponent } from './components/navigation/navigation.component';
import { LayoutModule } from '@angular/cdk/layout';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import {MatDialogModule} from '@angular/material/dialog';
import {MatStepperModule} from '@angular/material/stepper';
import { MatCardModule } from '@angular/material/card';
import {MatFormFieldModule, MAT_FORM_FIELD_DEFAULT_OPTIONS} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {MatAutocompleteModule} from '@angular/material/autocomplete';
import { MatTableModule } from '@angular/material/table';
import {MatMenuModule} from '@angular/material/menu';
import { MatChipsModule } from '@angular/material/chips';
import {MatPaginatorModule} from '@angular/material/paginator';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { SetlistCreatorComponent } from './components/setlist-creator/setlist-creator.component';
import { DragDropModule } from '@angular/cdk/drag-drop';
import { ScrollingModule } from '@angular/cdk/scrolling';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { LogComponent } from './components/log/log.component';
import { LyricsComponent } from './components/engine/components/lyrics/lyrics.component';
import { SetlistComponent } from './components/engine/components/setlist/setlist.component';
import { ButtonsComponent } from './components/engine/components/buttons/buttons.component';
import { StatusComponent } from './components/engine/components/status/status.component';
import { DebugComponent } from './components/engine/components/debug/debug.component';
import { WebSocketService } from './services/web-socket/web-socket.service';
import { DevicesComponent } from './components/devices/devices.component';
import { ToggleFullScreenDirective } from './toggle-full-screen.directive';
import { SongBookComponent } from './components/song-book/song-book.component';
import { HttpErrorHandler } from './services/http-error-handler.service';
import { CreateSongComponent } from './components/song-book/create-song/create-song.component';
import { ConfigureDeviceComponent } from './components/devices/configure-device/configure-device.component';
import { ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    AppComponent,
    EngineComponent,
    PageNotFoundComponent,
    NavigationComponent,
    SetlistCreatorComponent,
    LogComponent,
    LyricsComponent,
    SetlistComponent,
    ButtonsComponent,
    StatusComponent,
    DebugComponent,
    DevicesComponent,
    ToggleFullScreenDirective,
    SongBookComponent,
    CreateSongComponent,
    ConfigureDeviceComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    LayoutModule,
    MatToolbarModule,
    MatButtonModule,
    MatButtonToggleModule,
    MatSidenavModule,
    MatIconModule,
    MatStepperModule,
    MatListModule,
    MatMenuModule,
    MatDialogModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatAutocompleteModule,
    MatChipsModule,
    MatPaginatorModule,
    MatSlideToggleModule,
    MatProgressBarModule,
    DragDropModule,
    ScrollingModule,
    MatTableModule,
    ReactiveFormsModule
  ],
  providers: [
    WebSocketService,
    HttpErrorHandler,
    {provide: MAT_FORM_FIELD_DEFAULT_OPTIONS, useValue: {appearance: 'OUTLINE'}}
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
