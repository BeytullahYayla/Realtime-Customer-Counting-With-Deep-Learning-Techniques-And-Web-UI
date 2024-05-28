import React, { useState } from 'react';
import '../components/styles/Login.css';
import { BsPersonCircle } from 'react-icons/bs';
import EditIcon from '@mui/icons-material/Edit';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Cancel';
import { jwtDecode } from 'jwt-decode';
import axios from 'axios'

const Account = () => {
  const token = localStorage.getItem('access_token');
  const decodedToken = jwtDecode(token);

  const [userInfo, setUserInfo] = useState({
    username: decodedToken.username,
    email: decodedToken.email,
    password: "********",
    role: decodedToken.role
  });

  const [editMode, setEditMode] = useState({
    username: false,
    email: false,
    password: false,
  });

  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState('');

  const handleEdit = (field) => {
    setEditMode((prev) => ({ ...prev, [field]: true }));
  };

  const handleSave = async (field) => {
    try {
      if (field === 'password') {
        if (newPassword !== confirmNewPassword) {
          alert('New passwords do not match.');
          return;
        }

        const response = await axios.patch(`http://localhost:8000/users/${userInfo.username}/password`, {
          OldPassword: currentPassword,
          NewPassword: newPassword
        });

        alert(response.data.message);

        setUserInfo((prev) => ({ ...prev, password: '******' }));
        setCurrentPassword('');
        setNewPassword('');
        setConfirmNewPassword('');
      } else {
        const response = await axios.patch(`http://localhost:8000/users/${decodedToken.username}`, {
          Username: userInfo.username,
          Email: userInfo.email
        });

        const newToken = response.data.access_token;
        localStorage.setItem('access_token', newToken);
        localStorage.setItem('username', jwtDecode(newToken).username)

        setUserInfo((prev) => ({
          ...prev,
          username: jwtDecode(newToken).username,
          email: jwtDecode(newToken).email
        }));
      }
    } catch (error) {
      alert(`Failed to update ${field}: ${error.response ? error.response.data.detail : error.message}`);
    }
    setEditMode((prev) => ({ ...prev, [field]: false }));
  };

  const handleCancel = async (field) => {
    if (!editMode[field]) return;
    setEditMode((prev) => ({ ...prev, [field]: false }));
    setCurrentPassword('');
    setNewPassword('');
    setConfirmNewPassword('');
    const resetUserInfo = {
      username: decodedToken.username,
      email: decodedToken.email,
      password: "********",
      role: decodedToken.role
    };
    setUserInfo(resetUserInfo);
  };

  return (
    <main className='main-container'>
      <div className='main-title'>
        <h2>ACCOUNT MANAGEMENT</h2>
      </div>
      <div className="login-container" style={{ borderRadius: '3rem', margin: '0 auto', maxWidth: '30rem', padding: '3rem 6rem 5rem 6rem' }}>
        <BsPersonCircle className='login-icon' />
        <h2>{userInfo?.username}</h2>
        <div>
          <label htmlFor="username">Username</label>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <input
              type="text"
              id="username"
              value={userInfo.username}
              disabled={!editMode.username}
              onChange={(e) => setUserInfo({ ...userInfo, username: e.target.value })}
            />
            <div style={{
              color: '#ee7621',
              cursor: 'pointer',
              marginLeft: '1rem',
              marginBottom: '1rem',
              fontSize: '1.5rem',
              display: 'flex',
              alignItems: 'center'
            }}>
              {editMode.username ? (
                <>
                  <SaveIcon onClick={() => handleSave('username')} />
                  <CancelIcon style={{ marginLeft: '1rem' }} onClick={() => handleCancel('username')} />
                </>
              ) : (
                <EditIcon onClick={() => handleEdit('username')} />
              )}
            </div>
          </div>
        </div>
        <div>
          <label htmlFor="email">Email</label>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <input
              type="email"
              id="email"
              value={userInfo.email}
              disabled={!editMode.email}
              onChange={(e) => setUserInfo({ ...userInfo, email: e.target.value })}
            />
            <div style={{
              color: '#ee7621',
              cursor: 'pointer',
              marginLeft: '1rem',
              marginBottom: '1rem',
              fontSize: '1.5rem',
              display: 'flex',
              alignItems: 'center'
            }}>
              {editMode.email ? (
                <>
                  <SaveIcon onClick={() => handleSave('email')} />
                  <CancelIcon style={{ marginLeft: '1rem' }} onClick={() => handleCancel('email')} />
                </>
              ) : (
                <EditIcon onClick={() => handleEdit('email')} />
              )}
            </div>
          </div>
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <input
              type="password"
              id="password"
              value={userInfo.password}
              disabled
            />
            <div style={{
              color: '#ee7621',
              cursor: 'pointer',
              marginLeft: '1rem',
              marginBottom: '1rem',
              fontSize: '1.5rem',
              display: 'flex',
              alignItems: 'center'
            }}>
              {editMode.password ? (
                <>
                  <SaveIcon onClick={() => handleSave('password')} />
                  <CancelIcon style={{ marginLeft: '1rem' }} onClick={() => handleCancel('password')} />
                </>
              ) : (
                <EditIcon onClick={() => handleEdit('password')} />
              )}
            </div>
          </div>
          {editMode.password && (
            <div>
              <label htmlFor="currentPassword">Current Password</label>
              <input
                type="password"
                id="currentPassword"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                required
              />
              <label htmlFor="newPassword">New Password</label>
              <input
                type="password"
                id="newPassword"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
              />
              <label htmlFor="confirmNewPassword">Confirm New Password</label>
              <input
                type="password"
                id="confirmNewPassword"
                value={confirmNewPassword}
                onChange={(e) => setConfirmNewPassword(e.target.value)}
                required
              />
            </div>
          )}
        </div>
        <div>
          <label htmlFor="role">Role</label>
          <input
            style={{
              width: "calc(75% - 1.5rem)",
            }}
            type="text"
            id="role"
            value={userInfo.role}
            disabled
          />
        </div>
      </div>
    </main>
  );
};

export default Account;
