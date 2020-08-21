import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-actor',
  templateUrl: './actor.component.html',
  styleUrls: ['./actor.component.css']
})
export class ActorComponent implements OnInit {

  constructor(
    public name: string, 
    public age: number,
    public gender: string, 
    public imagelink: string,
    public catchprhase: string  

  ) { }

  ngOnInit(): void {
  }

}
