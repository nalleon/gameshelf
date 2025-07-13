package es.gameshelf.domain.interfaces.service;

import es.gameshelf.domain.Status;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
public interface IStatusService {
    Status add(String name, String description);
    List<Status> findAll();
    Status findById(Integer id);
    Status findByName(String name);
    boolean delete(Integer id);
    Status update(Integer id, String name, String description);
}
