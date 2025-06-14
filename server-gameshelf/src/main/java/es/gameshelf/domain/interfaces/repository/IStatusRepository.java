package es.gameshelf.domain.interfaces.repository;

import es.gameshelf.domain.Status;

import java.util.List;

public interface IStatusRepository {
    Status save(Status status);
    List<Status> findAll();
    Status findById(Integer id);
    Status findByName(String name);
    boolean delete(Integer id);
    Status update(Status status);
}
