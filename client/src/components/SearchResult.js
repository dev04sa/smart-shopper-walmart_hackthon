import React, { useState, useEffect } from 'react';
import SearchCard from './SearchCard';
import { useNavigate } from 'react-router-dom';

function SearchResult(props) {
  const getImageUrl = (id) => {
  const formats = ['jpg', 'jpeg', 'png'];
  for (let ext of formats) {
    const img = new Image();
    img.src = `/images/${id}.${ext}`;
    if (img.complete) return img.src;
  }
  return '/images/placeholder.jpg'; // fallback image
};
    const navigate = useNavigate();
    const [items, setItems] = useState([]);

    const fetchResult=async()=>{
        const str = localStorage.getItem('searchStr');
        const response = await fetch("http://127.0.0.1:8000/search", {
            method: "POST",
            headers: {"Content-Type": "application/x-www-form-urlencoded"},
            body: `searchStr=${encodeURIComponent(str)}`
        });
        if(response.status === 200){
            const results = await response.json();
            setItems(results.result);
        }
    };

    useEffect(()=>{
        fetchResult();
    }, [props.newSearch]);

    const [itemClicked, setItemClicked] = useState(false);
    useEffect(()=>{
      if(itemClicked)
        navigate('/itemdesc');
      //eslint-disable-next-line
    }, [itemClicked]);

  return (
    <div className="searchResult">
      {items.map((element)=>{
        return <SearchCard key={element.article_id} article_id={element.article_id} title={element.prod_name} price={element.price} desc={element.index_group_name} image={getImageUrl(element.article_id)} setItemClicked={setItemClicked} />
      })}
    </div>
  )
}

export default SearchResult;