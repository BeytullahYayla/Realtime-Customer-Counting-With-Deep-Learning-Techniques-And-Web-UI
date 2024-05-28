// src/components/Login.js
import React, { useState, useEffect } from 'react';
import './styles/Login.css';
import { BsPersonFillLock } from 'react-icons/bs'
import axios from 'axios';
import { setUserRole } from '../data/Fetch';
import { jwtDecode } from 'jwt-decode';
import { BsEye, BsEyeSlash } from 'react-icons/bs';

function Login({ handleLogin }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);

    useEffect(() => {
        const savedEmail = localStorage.getItem('email');
        if (savedEmail) {
            setEmail(savedEmail);
            handleLogin();
        }
    }, [handleLogin]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post('http://localhost:8000/login', {
                Email: email,
                Password: password
            });

            const { access_token } = response.data;

            setUserRole(jwtDecode(access_token).role);
            localStorage.setItem('username', jwtDecode(access_token).username);
            localStorage.setItem('access_token', access_token);
            handleLogin();
        } catch (error) {
            console.error('Login failed:', error);
            alert('Invalid login.');
        }
    };

    return (
        <div className="login-body">
            <div className="login-container">
                <BsPersonFillLock className='login-icon' />
                <h2>ADMIN PANEL</h2>
                <form onSubmit={handleSubmit}>
                    <label htmlFor="email">Email</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    <label htmlFor="password">Password</label>
                    <div style={{ position: 'relative' }}>
                        <input
                            type={showPassword ? "text" : "password"}
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                        <div
                            style={{
                                position: 'absolute',
                                top: '40%',
                                right: '4%',
                                transform: 'translateY(-50%)',
                                cursor: 'pointer',
                                color: '#ee7621 ',
                                fontSize: '1.8rem'
                            }}
                            onClick={() => setShowPassword(prev => !prev)}
                        >
                            {showPassword ? <BsEyeSlash />
                                : <BsEye />}
                        </div>
                    </div>
                    <button type="submit">Login</button>
                </form>
            </div>
        </div>
    );
}

export default Login;
