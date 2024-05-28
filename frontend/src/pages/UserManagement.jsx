import React, { useEffect, useState } from 'react'
import UserList from '../components/UserList'
import { useUsers, getUsers } from '../data/Fetch'
import Loading from '../components/Loading'
import CreateUser from '../components/CreateUser'
import Button from '@mui/material/Button';
import UndoIcon from '@mui/icons-material/Undo';
import PersonAddAlt1Icon from '@mui/icons-material/PersonAddAlt1';

const UserManagement = () => {

    const { fetchUsers } = useUsers()
    const users = getUsers()
    const [loading, setLoading] = useState(true);
    const [showCreateUser, setShowCreateUser] = useState(false);

    useEffect(() => {
        const fetchUsersAsync = async () => {
            try {
                await fetchUsers();
            } catch (error) {
                console.error("Veri çekme hatası:", error);
            } finally{
                setLoading(false)
            }
        };

        fetchUsersAsync();
    }, [fetchUsers, showCreateUser, loading]);

    if (loading) {
        return (
            <main className='main-container'>
                <Loading />
            </main>
        );
    }

    const handleToggleView = () => {
        setShowCreateUser(prevShowCreateUser => !prevShowCreateUser);
        if (showCreateUser) {
            setLoading(true);
        }
    };

    return (
        <main className='main-container'>
            <div className='main-title'>
                <h2>USER MANAGEMENT</h2>
                <Button
                    variant="contained"
                    startIcon={
                        <div style={{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            width: '3rem',
                            height: '3rem',
                            borderRadius: '50%',
                            backgroundColor: showCreateUser ? '#ff7f50' : '#20b2aa'
                        }}>
                            {showCreateUser ? <UndoIcon fontSize="medium" /> : <PersonAddAlt1Icon fontSize="medium" />}
                        </div>
                    }
                    onClick={handleToggleView}
                    sx={{
                        marginLeft: 'auto',
                        fontFamily: 'Archivo',
                        marginBottom: '1rem',
                        backgroundColor: showCreateUser ? '#ff3030' : '#008b8b',
                        borderRadius: '2rem',
                        '&:hover': {
                            backgroundColor: showCreateUser ? '#cd2626' : '#1c6071',
                        }
                    }}
                    size='small'
                >
                    {showCreateUser ? "BACK TO LIST" : "CREATE NEW USER"}
                </Button>
            </div>
            {showCreateUser ? <CreateUser /> : <UserList data={users} />}
        </main>
    )
}

export default UserManagement
