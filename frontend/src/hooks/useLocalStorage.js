import { useState } from 'react';

const useLocalStorage = (key, defaultValue) => {
  // Create state variable to store
  // localStorage value in state
  const [localStorageValue, setLocalStorageValue] = useState(() => {
    try {
      const value = localStorage.getItem(key);
      // If value is already present in
      // localStorage then return it

      // Else set default value in
      // localStorage and then return it
      if (value) {
        return JSON.parse(value);
      } else {
        if(defaultValue!==undefined){
          localStorage.setItem(key, JSON.stringify(defaultValue));
        return defaultValue;
        }
        
      }
    } catch (error) {
      if(defaultValue!==undefined){
      localStorage.setItem(key, JSON.stringify(defaultValue));
      return defaultValue;
      }
    }
  });

  // this method update our localStorage and our state
  const setLocalStorageStateValue = (valueOrFn) => {
    let newValue;
    if (typeof valueOrFn === 'function') {
      const fn = valueOrFn;
      newValue = fn(localStorageValue);
    } else {
      newValue = valueOrFn;
    }
    if(newValue !== undefined){
    localStorage.setItem(key, JSON.stringify(newValue));
    setLocalStorageValue(newValue);
    }
  };
  return [localStorageValue, setLocalStorageStateValue];
};

export default useLocalStorage;
