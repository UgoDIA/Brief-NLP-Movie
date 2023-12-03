import type { Component } from 'solid-js';
import './App.css'
import Navbar from './components/Navbar';

import MovieGrid from './components/MovieGrid';

const App: Component = () => {
  return (
    <>
    <Navbar/>
    <div class="App">
      <header class="text-center p-4">
          <h1 class="text-2xl font-bold">Classement basé sur le modèle bert-base-multilingual-uncased-sentiment</h1>
      </header>
      <main class="p-4">
        <MovieGrid />
      </main>
    </div>
    </>
  );
};

export default App;
