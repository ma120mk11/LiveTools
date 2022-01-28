import { DragDropModule } from '@angular/cdk/drag-drop';
import { waitForAsync, ComponentFixture, TestBed } from '@angular/core/testing';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { SetlistCreatorComponent } from './setlist-creator.component';

describe('SetlistCreatorComponent', () => {
  let component: SetlistCreatorComponent;
  let fixture: ComponentFixture<SetlistCreatorComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ SetlistCreatorComponent ],
      imports: [
        NoopAnimationsModule,
        DragDropModule,
      ]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SetlistCreatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should compile', () => {
    expect(component).toBeTruthy();
  });
});
