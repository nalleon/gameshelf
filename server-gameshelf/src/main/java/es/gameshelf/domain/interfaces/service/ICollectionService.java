package es.gameshelf.domain.interfaces.service;

import es.gameshelf.domain.Collection;
import es.gameshelf.domain.User;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
public interface ICollectionService {
    Collection add(User user);
    List<Collection> findAll();
    Collection findById(Integer id);
    List<Collection> findAllByUser(User user);
    boolean delete(Integer id);
    Collection update(Integer id, User user);
}
