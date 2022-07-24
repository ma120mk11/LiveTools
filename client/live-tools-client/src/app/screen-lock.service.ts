import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ScreenLockService {

  constructor() { }

  isScreenLockSupported() {
    return ('wakeLock' in navigator);
  }

  async getScreenLock() {
    if (this.isScreenLockSupported()) {
      let screenLock;
      try {
        // Typescript doesn't recognise the wakelock property on navigator
        const anyNav: any = navigator
        screenLock = await anyNav.wakeLock.request('screen');
      } catch (err: any) {
        console.log(err.name, err.message);
      }
      return screenLock;
    }
  }
}
