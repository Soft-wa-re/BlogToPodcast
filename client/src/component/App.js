import background from 'assets/roboTalk.png';
import './App.css';
import React, { useId, useState, useEffect } from 'react'

import { getFirestore, collection, addDoc, getDocs, doc, setDoc } from 'firebase/firestore/lite';
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getDatabase } from "firebase/database";

function App() {
  const id = useId();
  const [input, setInput] = useState('');
  async function postNewBlog() {
    const firebaseConfig = {
      apiKey: "AIzaSyAgtAivg3-Y_vDDIIrQdNXOMwGorUoBlLw",
      authDomain: "podcast-soft-wa-re.firebaseapp.com",
      databaseURL: "https://podcast-soft-wa-re-default-rtdb.firebaseio.com",
      projectId: "podcast-soft-wa-re",
      storageBucket: "podcast-soft-wa-re.appspot.com",
      messagingSenderId: "156098294079",
      appId: "1:156098294079:web:7a9abcec48fd5faf9ae38a",
      measurementId: "G-JXKNECLY5L"
    };

    const app = initializeApp(firebaseConfig);
    const analytics = getAnalytics(app);
    const db = getDatabase(app);
    const fs = getFirestore(app);

    const thing = collection(fs, 'blogs')
    const stuff = await getDocs(thing)

    var r = new RegExp(/(http(s?):\/\/)?(www\.)?github\.([a-z])+\/([A-Za-z0-9]{1,})+\/?/igm);
    if (r.test(input)) {
      const docRef = await addDoc(collection(fs, "blogs"), {
        url: input
      }).then(function () {
        window.alert("Success! We will be in touch!")
      }, function () {
        window.alert("An Unknown Error Occurred")
      });
    } else {
      window.alert("This is not a valid URL, please enter a fully qualified URL")
    }
  }

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
          value={input} onInput={e => setInput(e.target.value)}
          placeholder="github.com/tbeckenhauer/tbeckenhauer.github.io" />
        <button onClick={postNewBlog}>Subscribe!</button>
      </header>
    </div>
  );
}

export default App;
