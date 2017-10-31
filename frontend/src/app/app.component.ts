import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'app';
  mostrarNavbar = false;

  constructor(){
    
  }
    
  // ngOnInit(){
  //   this.authService.mostrarMenuEmitter.subscribe(
  //     mostrar => this.mostrarNavbar = mostrar
  //   );
  // }
  logout(){
    // this.authService.mostrarMenuEmitter.unsubscribe();
    this.mostrarNavbar = false;
  }
}
