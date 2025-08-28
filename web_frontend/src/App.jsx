import { useState } from "react";
import "./App.css";
import axios from "axios";

function App() {
  const [prediction, setPrediction] = useState([]);
  const [movieName, setMovieName] = useState("");
  const handleUpload = async () => {
    const response = await axios.post("http://127.0.0.1:8000/getBooks", {
      name: movieName,
    });
    setPrediction(response.data.recommendations);
  };
  return (
    <>
      <div className="container">
        <h1>Movie Recommender System</h1>
        <input
          type="text"
          className="input"
          onChange={(e) => setMovieName(e.target.value)}
        />
        <input
          className="submit"
          type="submit"
          value="recommend"
          onClick={handleUpload}
        />
        {prediction.length > 0 && (
          <div>
            <h1>Recommended Books:</h1>
            <ul className="book-list">
              {prediction.map((book, index) => (
                <li key={index} className="book-item">
                  <img
                    src={book.poster_url}
                    alt={book.name}
                    className="book-poster"
                  />
                  <span className="book-name">{book.name}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </>
  );
}

export default App;
