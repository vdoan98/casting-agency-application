
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { AuthService } from './auth.service';
import { environment } from 'starter/frontend/src/environments/environment';

export interface Movie{
    id: number;
    title: string;
    imagelink: string;
    year: number;
}

@Injectable({
    providedIn: 'root'
})
export class MoviesService{
    url = environment.apiServerUrl;

    public items: {[key: number]: Movie} = {};

    constructor(private auth: AuthService, private http:HttpClient) { }

    getHeaders() {
        const header = {
          headers: new HttpHeaders()
            .set('Authorization',  `Bearer ${this.auth.activeJWT()}`)
        };
        return header;
    }

    getMovies(){
        if (this.auth.can('get:movies')){
            this.http.get(this.url + '/movies', this.getHeaders())
            .subscribe((res: any) => {
                this.moviesToItems(res.drinks);
                console.log(res);
            });
        } 
    }

    saveMovie(movie: Movie) {
        if (movie.id >= 0){
            //patch 
            this.http.patch(this.url + '/movies/' + movie.id, movie, this.getHeaders())
            .subscribe( (res: any) => {
                if (res.success) {
                    this.moviesToItems(res.movies);
                }
            });  
        } else {
            //post 
            this.http.post(this.url + '/movies', movie, this.getHeaders())
            .subscribe( (res: any) => {
                if (res.success) {
                    this.moviesToItems(res.movies);
                }
            });
        }
    }

    deleteMovie(movie: Movie) {
        delete this.items[movie.id];
        this.http.delete(this.url + '/movies/' + movie.id, this.getHeaders())
        .subscribe( (res: any) => {

        });
    }


    moviesToItems( movies: Array<Movie>) {
        for (const movie of movies) {
          this.items[movie.id] = movie;
        }
    }


}