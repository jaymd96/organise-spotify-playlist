import axios from "axios";
import MockAdapter from "axios-mock-adapter";

const instance = axios.create({
    baseURL: "http://localhost:8888/api",
    timeout: 10000,
    headers: { "X-Custom-Header": "foobar" },
});

/* 
var mock = new MockAdapter(instance, { delayResponse: 2000 });

mock.onGet("/playlist").reply(200, {
    profile: {
        name: "James Mason-Drust", picture: "https://i.pinimg.com/originals/a8/bc/90/a8bc90ea196737604770aaf9c2d56a51.jpg"
    },
    summary: { playlists: 42, tracks: 1570, hours: 4.5 },
    playlists: [
        { name: "2022-04", tracks: 12, hours: 1.4 },
        { name: "2022-05", tracks: 23, hours: 0.23 },
        { name: "2022-06", tracks: 255, hours: 4.5 },
        { name: "2022-07", tracks: 350, hours: 6.7 },
    ],
});
 */

class Spotipy {
    static serverUrl() {
        return instance.defaults.baseURL
    }
    static async playlists() {
        return await instance.get("/playlist").then((resp) => resp.data);
    }

    static async makePlaylists() {
        return await instance.put("/playlist")
    }
}

export default Spotipy;