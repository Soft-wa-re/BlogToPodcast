import React from 'react';
import './Navigation.css';
import {
    Link
} from 'react-router-dom'

function Navigation () {
	return (
        <nav>
          <Link
              className="App-link"
              to="/">App</Link>
          <Link
              className="App-link"
              to="/about">About Us</Link>
        </nav>
	)
}
export default Navigation;
