import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SalaFormEditComponent } from './sala-form-edit.component';

describe('SalaFormEditComponent', () => {
  let component: SalaFormEditComponent;
  let fixture: ComponentFixture<SalaFormEditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SalaFormEditComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SalaFormEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
