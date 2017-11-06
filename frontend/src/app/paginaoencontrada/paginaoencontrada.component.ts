import { AuthGuard } from './../guards/auth.guard';
import { AuthService } from './../login/auth.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-paginaoencontrada',
  templateUrl: './paginaoencontrada.component.html',
  styleUrls: ['./paginaoencontrada.component.css']
})
export class PagiNaoEncontradaComponent implements OnInit {

  constructor(private authService:AuthService) { }

  ngOnInit() {
  }

}
