import { Directive, HostListener } from '@angular/core';
import screenfull from 'screenfull'

@Directive({
  selector: '[appToggleFullScreen]'
})
export class ToggleFullScreenDirective {
  
  @HostListener("click")
  onClick() {
    if (screenfull.isEnabled) {
      screenfull.toggle();
    }
  }

}
