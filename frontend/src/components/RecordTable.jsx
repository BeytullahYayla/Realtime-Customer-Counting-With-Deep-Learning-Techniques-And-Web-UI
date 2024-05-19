import React from 'react'
import { DataGrid, GridToolbarContainer, GridToolbarColumnsButton, GridToolbarFilterButton, GridToolbarDensitySelector, GridToolbarExport } from '@mui/x-data-grid';

const columns = [
    { field: 'id', headerName: '#', flex: 1, align: 'center', headerAlign: 'center' },
    { field: 'DateTime', headerName: 'Date', flex: 1, align: 'center', headerAlign: 'center' },
    { field: 'ManCount', headerName: 'Man', type: 'number', flex: 1, align: 'center', headerAlign: 'center' },
    { field: 'WomanCount', headerName: 'Woman', type: 'number', flex: 1, align: 'center', headerAlign: 'center' },
    { field: 'KidCount', headerName: 'Kid', type: 'number', flex: 1, align: 'center', headerAlign: 'center' },
    { field: 'StaffCount', headerName: 'Staff', type: 'number', flex: 1, align: 'center', headerAlign: 'center' },
    { field: 'EmployeeCount', headerName: 'Employee', type: 'number', flex: 1, align: 'center', headerAlign: 'center' },
    { field: 'TotalCount', headerName: 'Total', type: 'number', flex: 1, align: 'center', headerAlign: 'center' }
];

function CustomToolbar() {
    return (
        <GridToolbarContainer style={{ justifyContent: 'space-between' }} >
            <GridToolbarContainer>
                <GridToolbarDensitySelector style={{ color: '#1d2634', fontSize: 20, fontFamily: 'Oswald' }} />
                <GridToolbarColumnsButton style={{ color: '#1d2634', fontSize: 20, fontFamily: 'Oswald' }} />
                <GridToolbarFilterButton style={{ color: '#1d2634', fontSize: 20, fontFamily: 'Oswald' }} />
            </GridToolbarContainer>
            <GridToolbarExport style={{ color: '#1d2634', fontSize: 20, fontFamily: 'Oswald' }} />
        </GridToolbarContainer>
    );
}

const RecordTable = ({data}) => {
    const dataWithId = data.map((item, index) => ({ id: index + 1, ...item }));
    return (
        <div style={{ height: '90%', width: '90%', margin: '0 auto' }}>
            <DataGrid
                slots={{ toolbar: CustomToolbar }}
                sx={{ color: '#1d2634', backgroundColor: '#f0f0f0', fontSize: 18, fontFamily: 'Archivo' }}
                rows={dataWithId}
                columns={columns}
                density='compact'
                initialState={{
                    pagination: {
                        paginationModel: { page: 0, pageSize: 20 },
                    },
                }}
                /*columnVisibilityModel={{
                    id: false,
                }}*/
                pageSizeOptions={[7, 14, 20, 30]}
                checkboxSelection
            />
        </div>
    )
}

export default RecordTable