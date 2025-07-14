package es.gameshelf.domain.services;

import es.gameshelf.domain.Platform;
import es.gameshelf.domain.interfaces.repository.IPlatformRepository;
import es.gameshelf.domain.interfaces.repository.IPublisherRepository;
import es.gameshelf.domain.interfaces.service.IPlatformService;
import es.gameshelf.domain.interfaces.service.IPublisherService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
@Service
public class PlatformService implements IPlatformService {
    /**
     * Properties
     */
    IPlatformRepository repository;

    /**
     * Setter for the autowired service
     * @param repository of the service
     */
    @Autowired
    public void setRepository(IPlatformRepository repository) {
        this.repository = repository;
    }

    @Override
    public Platform add(String name) {
        Platform item = new Platform();
        item.setName(name);
        return repository.save(item);
    }

    @Override
    public List<Platform> findAll() {
        return repository.findAll();
    }

    @Override
    public Platform findById(Integer id) {
        return repository.findById(id);
    }

    @Override
    public Platform findByName(String name) {
        return repository.findByName(name);
    }

    @Override
    public boolean delete(Integer id) {
        return repository.delete(id);
    }

    @Override
    public Platform update(Integer id, String name) {
        Platform item = new Platform(id);
        item.setName(name);
        return repository.save(item);    }
}
