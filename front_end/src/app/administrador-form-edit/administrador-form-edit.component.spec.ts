import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AdministradorFormEditComponent } from './administrador-form-edit.component';

describe('AdministradorFormEditComponent', () => {
  let component: AdministradorFormEditComponent;
  let fixture: ComponentFixture<AdministradorFormEditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AdministradorFormEditComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdministradorFormEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
