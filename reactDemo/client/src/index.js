import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Router from './Router';

export let FINNISH_MODE = true;

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  // <React.StrictMode>
    <Router />
  // </React.StrictM  ode>
);

