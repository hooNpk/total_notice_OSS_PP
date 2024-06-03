import React, { useEffect, useState } from 'react';
import MUIDataTable from "mui-datatables";

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/data')
      .then(response => response.json())
      .then(data => setData(data));
  }, []);

  const columns = [
    {
      name: "title",
      label: "Title",
      options: {
        filter: false
      }
    },
    {
      name: "ctgry",
      label: "Category",
      options: {
        filter: true
      }
    },
    {
      name: "date",
      label: "Date",
      options: {
        filter: true
      }
    },
    {
      name: "writer",
      label: "Writer",
      options: {
        filter: false
      }
    },
    {
      name: "source",
      label: "Source",
      options: {
        filter: true
      }
    }
  ];
  
  const options = {
    filterType: 'checkbox',
    onRowClick: (rowData, rowMeta) => {
      // rowData는 선택된 행의 데이터 배열, rowMeta는 행의 메타데이터
      const url = data[rowMeta.dataIndex].url; // URL을 데이터 배열에서 추출
      window.open(url, '_blank'); // 새 탭에서 URL 열기
    }
  };

  return (
    <div className="App">
      <MUIDataTable
        title={"Total Notice"}
        data={data.map(
          item => [item.title, item.ctgry, item.date, item.writer, item.source]
        )}
        columns={columns}
        options={options}
      />
    </div>
  );
}

export default App;
