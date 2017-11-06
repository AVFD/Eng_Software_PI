import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SalasFormComponent } from './salas-form.component';

describe('SalasFormComponent', () => {
  let component: SalasFormComponent;
  let fixture: ComponentFixture<SalasFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SalasFormComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SalasFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
