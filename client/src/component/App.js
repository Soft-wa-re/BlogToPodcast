import background from 'assets/roboTalk.png';
import './App.css';
import React, { useState, useEffect } from 'react'

function App() {
  const [data, setData] = useState([{}])
  useEffect(() => {
    fetch("/members").then(
        res => res.json()
    ).then(
        data => {
            setData(data)
        }
    )
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <img src={background} className="App-logo" alt="logo" />
        <p>
            Subscribe to receive PRs for your very own podcast.
        </p>
        <input
            className="App-inputfield"
            placeholder="github.com/tbeckenhauer/tbeckenhauer.github.io"/>
        <button>Subscribe!</button>
      </header>
    </div>
  );
}

export default App;
