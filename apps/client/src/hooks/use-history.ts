import { fetchHistory } from "@/api/history";
import { useQuery } from "@tanstack/react-query";

export default function useHistory() {
  return useQuery({
    queryKey: ['weather', 'history'],
    queryFn: () => fetchHistory(),
  });
}