import { Router } from '@angular/router';
import { SalasService } from './../salas/salas.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-salas-form',
  templateUrl: './salas-form.component.html',
  styleUrls: ['./salas-form.component.css']
})
export class SalasFormComponent implements OnInit {
  private sala:any = {}
  constructor(private route:Router, private salasService:SalasService) { }

  ngOnInit() {
  }
  onSubmit(form){
    if(form.valid){
      this.sala = {
        'name': form.value.name
      }
      this.salasService.adicionarSala(this.sala).subscribe();
      this.route.navigate(['/salas']);
    }
    else{
      this.route.navigate(['/erro']);
    }

  }
}
