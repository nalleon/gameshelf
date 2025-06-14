package es.gameshelf.domain.interfaces.repository;

import es.gameshelf.domain.Collection;
import es.gameshelf.domain.Game;
import es.gameshelf.domain.User;

import java.util.List;

public interface ICollectionRepository {
    Collection save(Collection collection);
    List<Collection> findAll();
    Collection findById(Integer id);
    List<Collection> findAllByUser(User user);
    boolean delete(Integer id);
    Collection update(Collection collection);
}
