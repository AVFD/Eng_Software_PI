import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { UsrFormComponent } from './usr-form.component';

describe('UsrFormComponent', () => {
  let component: UsrFormComponent;
  let fixture: ComponentFixture<UsrFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ UsrFormComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UsrFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
