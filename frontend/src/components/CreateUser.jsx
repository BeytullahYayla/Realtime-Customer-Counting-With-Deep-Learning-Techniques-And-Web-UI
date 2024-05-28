import React, { useState } from 'react';
import './styles/Login.css';
import axios from 'axios';
import { BsPersonPlusFill, BsEye, BsEyeSlash } from 'react-icons/bs';

function CreateUser() {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [role, setRole] = useState("Admin");
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (password !== confirmPassword) {
            alert('Passwords do not match.');
            return;
        }

        try {
            await axios.post('http://localhost:8000/register', {
                Username: username,
                Email: email,
                Password: password,
                SuperUser: (role === 'SuperUser' ? true : false)
            });

            alert('User created successfully.');
        } catch (error) {
            console.error('User creation failed:', error);
            alert('Failed to create user.');
        }
    };

    return (
        <div className="login-container" style={{ margin: '0 auto', maxWidth: '30rem', padding: '2rem 6rem' }}>
            <BsPersonPlusFill className='login-icon' />
            <h2>CREATE USER</h2>
            <form onSubmit={handleSubmit}>
                <label htmlFor="username">Username</label>
                <input
                    type="text"
                    id="username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
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
                <label htmlFor="confirmPassword">Confirm Password</label>
                <div style={{ position: 'relative' }}>
                    <input
                        type={showConfirmPassword ? "text" : "password"}
                        id="confirmPassword"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
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
                        onClick={() => setShowConfirmPassword(prev => !prev)}
                    >
                        {showConfirmPassword ? <BsEyeSlash /> 
                        : <BsEye />}
                    </div>
                </div>
                <label htmlFor="role">Role</label>
                <select
                    id="role"
                    value={role}
                    onChange={(e) => setRole(e.target.value)}
                    required
                    style={{
                        width: "calc(75% - 1.5rem)",
                        padding: '0.75rem',
                        marginBottom: '1rem',
                        border: '1px solid #ddd',
                        borderRadius: '8px',
                        fontSize: '1rem',
                    }}
                >
                    <option value="Admin">Admin</option>
                    <option value="SuperUser">SuperUser</option>
                </select>
                <button type="submit">Create User</button>
            </form>
        </div>
    );
}

export default CreateUser;
