import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Card,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  CircularProgress,
} from "@mui/material";
import Sidebar from "../components/Sidebar"; // Adjust path as necessary
import axios from "axios";

const TeacherDashboard = () => {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStudents = async () => {
      try {


        
        // Retrieve teacher ID from sessionStorage
        const teacherSession = JSON.parse(sessionStorage.getItem("user"));

        if (teacherSession && teacherSession.id) {
          const teacherId = teacherSession.id;

          // Fetch students for the teacher
          const response = await axios.get(
            `http://127.0.0.1:8000/users/students/get_all_students_teacher_based/?teacher_id=${teacherId}`
          );

          setStudents(response.data);
        } else {
          console.error("Teacher ID not found in session.");
        }
      } catch (error) {
        console.error("Error fetching students:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchStudents();
  }, []);

  return (
    <Box
      sx={{
        display: "flex",
        minHeight: "100vh",
        backgroundColor: "#f4f6f8",
        padding: 3,
      }}
    >
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <Box sx={{ flex: 1, ml: "250px", p: 3 }}>
        <Typography
          variant="h4"
          sx={{
            textAlign: "center",
            fontWeight: "bold",
            color: "#001E3C",
            mb: 4,
          }}
        >
          Teacher Dashboard
        </Typography>

        <Card
          sx={{
            padding: 3,
            borderRadius: "12px",
            boxShadow: "0 4px 15px rgba(0, 0, 0, 0.2)",
            backgroundColor: "#fff",
          }}
        >
          <Typography
            variant="h6"
            sx={{
              mb: 2,
              fontWeight: "bold",
              color: "#0288d1",
            }}
          >
            Student List
          </Typography>

          {/* Loading Spinner */}
          {loading ? (
            <Box
              sx={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                minHeight: "200px",
              }}
            >
              <CircularProgress />
            </Box>
          ) : (
            <TableContainer component={Paper} sx={{ mt: 3 }}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell sx={{ fontWeight: "bold" }}>ID</TableCell>
                    <TableCell sx={{ fontWeight: "bold" }}>Username</TableCell>
                    <TableCell sx={{ fontWeight: "bold" }}>Email</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {students.map((student) => (
                    <TableRow key={student.id}>
                      <TableCell>{student.id}</TableCell>
                      <TableCell>{student.username}</TableCell>
                      <TableCell>{student.email}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </Card>
      </Box>
    </Box>
  );
};

export default TeacherDashboard;
