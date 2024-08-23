import { jwtDecode } from "jwt-decode";

export const checkAuth = () => {
    // Check if the user is authenticated using localStorage
    const token = localStorage.getItem('token');

    if (token) return true;
    return false;
}

const isTokenExpired = () => {
    const token = localStorage.getItem('token');
    if (!token || token === 'undefined') {
        return true; // No token, treat it as expired
    }
    try {
        const { exp } = jwtDecode(token);
        
        // Get the current time in seconds since the epoch
        const currentTime = Math.floor(Date.now() / 1000);
        
        // Check if the token is expired
        if (exp < currentTime) {
            console.log('Token is expired')
            return true;
        }
        
        return false; // Token is still valid
    } catch (e) {
        console.error('Error decoding token:', e);
        return true; // If decoding fails, treat it as expired
    }
};

export default isTokenExpired;




export const isTokenAboutToExpire = () => {
    const token = localStorage.getItem('token');
    if (!token || token === 'undefined') {
        return true; // No token, treat it as about to expire
    }
    
    try {
        const { exp } = jwtDecode(token);

        // Get the current time in seconds since the epoch
        const currentTime = Math.floor(Date.now() / 1000);

        // Calculate the time 5 seconds from now
        const fiveSecondsFromNow = currentTime + 5;

        // Check if the token is about to expire within the next 5 seconds
        if (exp < fiveSecondsFromNow) {
            return true;
        }

        return false; // Token is not about to expire
    } catch (e) {
        console.error('Error decoding token:', e);
        return true; // If decoding fails, treat it as about to expire
    }
};


