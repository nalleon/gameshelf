package es.gameshelf.domain.interfaces.repository;

import es.gameshelf.domain.Publisher;

import java.util.List;
/**
 * @author Nabil L. A. @nalleon
 */
public interface IPublisherRepository {
    Publisher save(Publisher publisher);
    List<Publisher> findAll();
    Publisher findById(Integer id);
    Publisher findByName(String name);
    boolean delete(Integer id);
    Publisher update(Publisher publisher);
}
