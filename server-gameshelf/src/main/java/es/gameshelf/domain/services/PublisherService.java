package es.gameshelf.domain.services;

import es.gameshelf.domain.Publisher;
import es.gameshelf.domain.interfaces.repository.IPublisherRepository;
import es.gameshelf.domain.interfaces.service.IPublisherService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
@Service
public class PublisherService implements IPublisherService {
    /**
     * Properties
     */
    IPublisherRepository repository;

    /**
     * Setter for the autowired service
     * @param repository of the service
     */
    @Autowired
    public void setRepository(IPublisherRepository repository) {
        this.repository = repository;
    }

    @Override
    public Publisher add(String name) {
        Publisher item = new Publisher();
        item.setName(name);
        return repository.save(item);
    }

    @Override
    public List<Publisher> findAll() {
        return repository.findAll();
    }

    @Override
    public Publisher findById(Integer id) {
        return repository.findById(id);
    }

    @Override
    public Publisher findByName(String name) {
        return repository.findByName(name);
    }

    @Override
    public boolean delete(Integer id) {
        return repository.delete(id);
    }

    @Override
    public Publisher update(Integer id, String name) {
        Publisher item = new Publisher(id);
        item.setName(name);
        return repository.save(item);    }
}
