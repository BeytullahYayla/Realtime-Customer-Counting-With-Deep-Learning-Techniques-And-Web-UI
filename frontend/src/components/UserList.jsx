import React, { useState } from 'react';
import { DataGrid, GridToolbarContainer, GridToolbarColumnsButton, GridToolbarFilterButton, GridToolbarDensitySelector, GridToolbarExport } from '@mui/x-data-grid';
import Button from '@mui/material/Button';
import axios from 'axios'

const CustomToolbar = () => (
    <GridToolbarContainer style={{ justifyContent: 'space-between' }} >
        <GridToolbarContainer>
            <GridToolbarDensitySelector style={{ color: '#1d2634', fontSize: 20, fontFamily: 'Oswald' }} />
            <GridToolbarColumnsButton style={{ color: '#1d2634', fontSize: 20, fontFamily: 'Oswald' }} />
            <GridToolbarFilterButton style={{ color: '#1d2634', fontSize: 20, fontFamily: 'Oswald' }} />
        </GridToolbarContainer>
        <GridToolbarContainer>
            <GridToolbarExport style={{ color: '#1d2634', fontSize: 20, fontFamily: 'Oswald' }} />
        </GridToolbarContainer>
    </GridToolbarContainer>
);

const UserList = ({ data }) => {
    const [rows, setRows] = useState(data.map((item, index) => ({ id: index + 1, ...item })));

    const handleRoleChange = async (id, newRole) => {
        const row = rows.find(row => row.id === id);
        try {
            await axios.patch(`http://localhost:8000/users/${row.Username}/toggle-role`);
            setRows((prevRows) => prevRows.map((row) => (
                row.id === id ? { ...row, Role: newRole } : row
            )));
        } catch (error) {
            console.error("Error changing user role:", error);
        }
    };

    const handleEnableChange = async (id) => {
        const row = rows.find(row => row.id === id);
        try {
            await axios.patch(`http://localhost:8000/users/${row.Username}/toggle-activation`);
            setRows((prevRows) => prevRows.map((row) => (
                row.id === id ? { ...row, IsEnable: row.IsEnable === 'Enabled' ? 'Disabled' : 'Enabled' } : row
            )));
        } catch (error) {
            console.error("Error changing user activation:", error);
        }
    };

    const columns = [
        { field: 'id', headerName: '#', flex: 0.5, align: 'center', headerAlign: 'center' },
        { field: 'Username', headerName: 'Username', flex: 1, align: 'center', headerAlign: 'center' },
        { field: 'Email', headerName: 'Email', flex: 1.5, align: 'center', headerAlign: 'center' },
        { field: 'Role', headerName: 'Role', flex: 1, align: 'center', headerAlign: 'center' },
        { field: 'IsEnable', headerName: 'Is Enable?', flex: 1, align: 'center', headerAlign: 'center' },
        {
            field: 'changeRole', headerName: 'Change Role', flex: 1, align: 'center', headerAlign: 'center',
            renderCell: (params) => (
                <div>
                    <Button
                        variant="contained"
                        color={params.row.Role === 'SuperUser' ? 'secondary' : 'primary'}
                        style={{ fontFamily: "Archivo" }}
                        onClick={() => handleRoleChange(params.id, params.row.Role === 'Admin' ? 'SuperUser' : 'Admin')}
                    >
                        {params.row.Role === 'Admin' ? 'Make SuperUser' : 'Make Admin'}
                    </Button>
                </div>
            )
        },
        {
            field: 'toggleEnable', headerName: 'Toggle Enable', flex: 1, align: 'center', headerAlign: 'center',
            renderCell: (params) => (
                <Button
                    variant="contained"
                    color={params.row.IsEnable === 'Enabled' ? 'error' : 'success'}
                    style={{ fontFamily: "Archivo" }}
                    onClick={() => handleEnableChange(params.id)}
                >
                    {params.row.IsEnable === 'Enabled' ? 'Disable' : 'Enable'}
                </Button>
            )
        }
    ];

    return (
        <div style={{ height: '90%', width: '90%', margin: '0 auto' }}>
            <DataGrid
                rows={rows}
                columns={columns}
                slots={{ toolbar: CustomToolbar }}
                sx={{ color: '#1d2634', backgroundColor: '#f0f0f0', fontSize: 18, fontFamily: 'Archivo' }}
                density='standard'
                initialState={{
                    pagination: {
                        paginationModel: { page: 0, pageSize: 10 },
                    },
                }}
                pageSizeOptions={[10, 20, 50]}
                checkboxSelection
                slotProps={{
                    pagination: {
                        sx: {
                            '& .MuiTablePagination-displayedRows': {
                                color: '#1d2634', fontFamily: 'Archivo'
                            },
                            '& .MuiTablePagination-selectLabel': {
                                color: '#1d2634', fontFamily: 'Archivo'
                            },
                        },
                    },
                }}
            />
        </div>
    );
};

export default UserList;
