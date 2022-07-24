import { TestBed } from '@angular/core/testing';

import { ScreenLockService } from './screen-lock.service';

describe('ScreenLockService', () => {
  let service: ScreenLockService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ScreenLockService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
