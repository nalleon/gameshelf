package es.gameshelf.domain.services;

import es.gameshelf.domain.Collection;
import es.gameshelf.domain.User;
import es.gameshelf.domain.interfaces.repository.ICollectionRepository;
import es.gameshelf.domain.interfaces.service.ICollectionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
@Service
public class CollectionService implements ICollectionService {

    /**
     * Properties
     */
    ICollectionRepository repository;

    /**
     * Setter for the autowired service
     * @param repository of the service
     */
    @Autowired
    public void setRepository(ICollectionRepository repository) {
        this.repository = repository;
    }

    @Override
    public Collection add(User user) {
        Collection item = new Collection();
        item.setUser(user);
        return repository.save(item);
    }

    @Override
    public List<Collection> findAll() {
        return repository.findAll();
    }

    @Override
    public Collection findById(Integer id) {
        return repository.findById(id);
    }

    @Override
    public boolean delete(Integer id) {
        return repository.delete(id);
    }

    @Override
    public Collection update(Integer id, User user) {
        Collection item = new Collection(id);
        item.setUser(user);
        return repository.update(item);
    }
}
