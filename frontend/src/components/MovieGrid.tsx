import { createResource, For } from 'solid-js';
import type { Component } from 'solid-js';

interface Movie {
    id_movie: number;
    movie_title: string;
    movie_rank: number;
    movie_score_press: string;
    movie_score_spectator: string;
    nlp_score_bert: string;
    nlp_rank_bert: number;
}

const fetchMovies = async (): Promise<Movie[]> => {
    const response = await fetch('https://nlp-movies.azurewebsites.net/get-movies/');
    return response.json();
};

const MovieGrid: Component = () => {
    const [movies] = createResource<Movie[]>(fetchMovies);

    const getPosterUrl = (id: number) => `/assets/${id}.jpg`;

    return (
        <div class="grid grid-cols-2 gap-4">
            <For each={movies()?.sort((a, b) => a.nlp_rank_bert - b.nlp_rank_bert).slice(0, 10)}>
                {(movie) => (
                    <div class="border p-4 flex flex-col items-center">
                        <span class="text-4xl p-3 font-bold">#{movie.nlp_rank_bert}</span>
                        <h2 class="mb-1 text-4xl font-bold">{movie.movie_title}</h2>
                        <div class="flex items-center space-x-4">
                            <img src={getPosterUrl(movie.id_movie)} alt={movie.movie_title} class="h-25 w-auto" />
                            <div class='text-left'>
                                <p class=" text-3xl">Score global: <b> {movie.nlp_score_bert}</b> </p>
                                <p class=" text-3xl">Ancien classement: <b>{movie.movie_rank}</b></p>
                                <p class=" text-3xl">Ancien score global: <b>{movie.movie_score_spectator}</b></p>
                            </div>
                        </div>
                    </div>
                )}
            </For>
        </div>
    );
};

export default MovieGrid;