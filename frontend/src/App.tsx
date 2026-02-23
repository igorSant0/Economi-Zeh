import { useUsers } from "@/hooks/user.hook";

function App() {
  // O React Query retorna 'data', que renomeamos para 'response' para não confundir 
  // com o array 'data' que vem de dentro do seu UserListResponse
  const { data: response, isLoading, isError } = useUsers();

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>💸 Economi-Zeh</h1>
      <h2>Usuários Cadastrados</h2>

      {isLoading && <p>Carregando dados do servidor...</p>}

      {isError && (
        <div style={{ color: "red", marginTop: "1rem" }}>
          <p><strong>Erro ao conectar com o backend.</strong></p>
          <p>Verifique se:</p>
          <ul>
            <li>O FastAPI e o Banco de Dados estão rodando.</li>
            <li>O CORS foi liberado no `app.py` do backend.</li>
          </ul>
        </div>
      )}

      {/* Acessamos response.data porque o seu schema define um objeto com a propriedade 'data' contendo o array */}
      {response?.data && (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {response.data.map((user) => (
            <li 
              key={user.id_user} 
              style={{ padding: "10px", borderBottom: "1px solid #ccc", marginBottom: "10px" }}
            >
              <strong>{user.user_name}</strong> <br />
              <small>Email: {user.user_email}</small> <br />
              <small>CPF: {user.user_cpf}</small>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;