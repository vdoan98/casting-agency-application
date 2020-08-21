import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { AuthService } from './auth.service';
import { environment } from 'starter/frontend/src/environments/environment';

export interface Actor {
    id: number, 
    name: string, 
    gender: string, 
    age: number,
    imagelink:string, 
    catchphrase:string 
}

@Injectable({
    providedIn: 'root'
})
export class ActorsService {
    url = environment.apiServerUrl;

    public items: {[key: number]: Actor} = {};

    constructor(private auth: AuthService, private http: HttpClient) { }

    getHeaders() {
        const header = {
            headers: new HttpHeaders()
              .set('Authorization',  `Bearer ${this.auth.activeJWT()}`)
        };
        return header;
    }

    getActors(){
        if (this.auth.can('get:actors')) {
            this.http.get(this.url + '/actors', this.getHeaders())
            .subscribe((res: any) => {
                this.actorsToItems(res.actors);
                console.log(res);
            });
        }
    }

    saveActor(actor: Actor) {
        if (actor.id >= 0) {
            //patch 
            this.http.patch(this.url + '/actors/' + actor.id, actor, this.getHeaders())
            .subscribe( (res: any) => {
                if (res.success) {
                    this.actorsToItems(res.actors);
                }
            });
        } else {
            //post 
            this.http.post(this.url + '/actors', actor, this.getHeaders())
            .subscribe( (res: any) => {
                if (res.success) {
                    this.actorsToItems(res.actors);
                }
            });
        }
    }

    deleteActor(actor: Actor){
        delete this.items[actor.id];
        this.http.delete(this.url + '/actors/' + actor.id, this.getHeaders())
        .subscribe( (res: any) => {

        });
    }

    actorsToItems( actors: Array<Actor>) {
        for (const actor of actors) {
          this.items[actor.id] = actor;
        }
      }

}