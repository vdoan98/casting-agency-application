import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-movie',
  templateUrl: './movie.component.html',
  styleUrls: ['./movie.component.css']
})
export class MovieComponent implements OnInit {

  constructor(
    public title: string, 
    public imagelink: string,
    public year: number
  ) { }

  ngOnInit(): void {
  }

}
