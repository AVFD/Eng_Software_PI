import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PaginaoencontradaComponent } from './paginaoencontrada.component';

describe('PaginaoencontradaComponent', () => {
  let component: PaginaoencontradaComponent;
  let fixture: ComponentFixture<PaginaoencontradaComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PaginaoencontradaComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PaginaoencontradaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
