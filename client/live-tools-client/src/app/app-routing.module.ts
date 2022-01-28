import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DevicesComponent } from './components/devices/devices.component';
import { ButtonsComponent } from './components/engine/components/buttons/buttons.component';
import { DebugComponent } from './components/engine/components/debug/debug.component';
import { LyricsComponent } from './components/engine/components/lyrics/lyrics.component';
import { SetlistComponent } from './components/engine/components/setlist/setlist.component';
import { StatusComponent } from './components/engine/components/status/status.component';
import { EngineComponent } from './components/engine/engine.component';
import { LogComponent } from './components/log/log.component';
import { PageNotFoundComponent } from './components/page-not-found/page-not-found.component';
import { SetlistCreatorComponent } from './components/setlist-creator/setlist-creator.component';
import { SongBookComponent } from './components/song-book/song-book.component';

const routes: Routes = [
  { path: 'engine', component: EngineComponent, 
  children:[
    { path: 'lyrics', component: LyricsComponent },
    { path: 'setlist', component: SetlistComponent },
    { path: 'debug', component: DebugComponent },
    { path: 'status', component: StatusComponent },
    { path: 'buttons', component: ButtonsComponent },
    { path: '**', component: SetlistComponent },
  ]},
  { path: 'setlist/create', component: SetlistCreatorComponent },
  { path: 'devices', component: DevicesComponent },
  { path: 'songs', component: SongBookComponent },
  { path: 'logs', component: LogComponent },
  { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
